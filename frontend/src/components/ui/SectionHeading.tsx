export const SectionHeading = ({
  eyebrow,
  title,
  body,
}: {
  eyebrow?: string;
  title: string;
  body?: string;
}) => (
  <div className="mx-auto max-w-3xl text-center">
    <p className="text-sm font-black uppercase tracking-[.22em] text-brandOrange">
      {eyebrow}
    </p>

    <h2 className="mt-3 text-3xl font-black tracking-tight text-ink md:text-5xl">
      {title}
    </h2>

    {body && (
      <p className="mt-4 text-lg leading-8 text-slate-600">
        {body}
      </p>
    )}
  </div>
);