import { DashboardLayout } from '../components/dashboard/DashboardLayout';
import { FormAnalysisUploader } from '../components/forms/FormAnalysisUploader';

export const FormAnalysisPage = () => (
  <DashboardLayout>
    <h1 className="text-4xl font-black">AI Form Analysis</h1>

    <p className="mt-2 max-w-3xl text-slate-600">
      Upload user technique media and compare against admin-approved
      references. Images are scored instantly; video files are stored for
      coach review and future frame analysis.
    </p>

    <div className="mt-8">
      <FormAnalysisUploader />
    </div>
  </DashboardLayout>
);