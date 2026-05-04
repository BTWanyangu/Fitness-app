import { useEffect, useMemo, useState } from 'react';
import { api } from '../../services/api';
import { Button } from '../ui/Button';
import { useAuth } from '../../contexts/AuthContext';

type ExerciseOption = { id: number; name: string; body_part: string; target_muscle: string };

export const FormAnalysisUploader = () => {
  const { isAuthenticated, user } = useAuth();
  const [exercises, setExercises] = useState<ExerciseOption[]>([]);
  const [exercise, setExercise] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [poseStatus, setPoseStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/exercises/').then((res) => setExercises(res.data.results || res.data)).catch(() => setExercises([]));
    api.get('/pose/status/').then((res) => setPoseStatus(res.data.pose_engine)).catch(() => setPoseStatus(null));
  }, []);

  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : ''), [file]);
  const isVideo = file?.type.startsWith('video/');

  const submit = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const fd = new FormData();
      fd.append('uploaded_file', file);
      if (exercise) fd.append('exercise', exercise);
      fd.append('user_name', isAuthenticated ? user?.full_name || user?.email || 'Authenticated User' : 'Guest User');
      const res = await api.post('/form-submissions/', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      setResult(res.data);
    } catch (err: any) {
      const data = err?.response?.data;
      setError(typeof data === 'object' ? JSON.stringify(data) : 'Analysis failed. Please check the file and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="rounded-3xl bg-white p-6 shadow-soft">
        <h2 className="text-2xl font-black">Upload your form</h2>
        <p className="mt-2 text-slate-600">Use a clear full-body image or short video. The backend compares your visible landmarks against admin-approved standards and reference media.</p>

        <div className={`mt-5 rounded-2xl p-4 text-sm font-bold ${poseStatus?.exists ? 'bg-green-50 text-brandGreen' : 'bg-orange-50 text-brandOrange'}`}>
          Pose model: {poseStatus?.exists ? 'ready' : 'fallback mode'}
        </div>

        <select className="mt-5 w-full rounded-2xl border p-4" value={exercise} onChange={(e) => setExercise(e.target.value)}>
          <option value="">Select exercise</option>
          {exercises.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>

        <label className="mt-4 flex min-h-40 cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed border-green-200 bg-green-50/60 p-5 text-center transition hover:bg-green-50">
          <input className="hidden" type="file" accept="image/*,video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <b className="text-brandGreen">Choose image or video</b>
          <span className="mt-2 text-sm text-slate-600">Recommended: full body visible, good lighting, stable camera.</span>
          {file && <span className="mt-3 rounded-full bg-white px-4 py-2 text-xs font-black text-slate-700">{file.name}</span>}
        </label>

        {previewUrl && (
          <div className="mt-5 overflow-hidden rounded-3xl border bg-slate-50">
            {isVideo ? <video src={previewUrl} className="max-h-80 w-full object-contain" controls /> : <img src={previewUrl} className="max-h-80 w-full object-contain" />}
          </div>
        )}

        {error && <div className="mt-4 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700">{error}</div>}
        <Button className="mt-5 rounded-xl" onClick={submit} disabled={!file || loading}>{loading ? 'Analyzing...' : 'Analyze Technique'}</Button>
      </div>

      <div className="rounded-3xl bg-white p-6 shadow-soft">
        <h2 className="text-2xl font-black">AI-assisted feedback</h2>
        {result ? (
          <>
            <div className="mt-5 flex items-end gap-2"><span className="text-6xl font-black text-brandGreen">{Math.round(result.score)}</span><span className="pb-2 text-xl font-black text-slate-500">/100</span></div>
            <p className="mt-3 text-slate-600">{result.analysis_summary}</p>

            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl bg-green-50 p-4"><b>Detected landmarks</b><p className="mt-2 text-sm text-slate-600">{Object.keys(result.detected_landmarks || {}).length || 0} visible landmarks mapped.</p></div>
              <div className="rounded-2xl bg-orange-50 p-4"><b>Angle checks</b><p className="mt-2 text-sm text-slate-600">{(result.angle_results || []).length} configured standards evaluated.</p></div>
            </div>

            <ul className="mt-4 space-y-3">{(result.feedback || []).map((item: string) => <li key={item} className="rounded-2xl bg-green-50 p-4 text-sm text-slate-700">{item}</li>)}</ul>

            {result.angle_results?.length ? (
              <div className="mt-5 overflow-hidden rounded-2xl border">
                <table className="w-full text-sm">
                  <thead className="bg-slate-50"><tr><th className="p-3 text-left">Angle</th><th className="p-3 text-left">Measured</th><th className="p-3 text-left">Expected</th><th className="p-3 text-left">Status</th></tr></thead>
                  <tbody>{result.angle_results.map((angle: any) => <tr key={angle.name} className="border-t"><td className="p-3 font-bold">{angle.name}</td><td className="p-3">{angle.measured}°</td><td className="p-3">{angle.expected_min}° - {angle.expected_max}°</td><td className="p-3 capitalize">{angle.status}</td></tr>)}</tbody>
                </table>
              </div>
            ) : null}
          </>
        ) : (
          <p className="mt-5 text-slate-600">Your score, landmark count, angle comparison and coaching feedback will appear here after upload.</p>
        )}
      </div>
    </div>
  );
};
