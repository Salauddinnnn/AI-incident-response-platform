function getSection(text = "", heading, nextHeading) {
  const start = text.indexOf(heading);

  if (start === -1) return "";

  const contentStart = start + heading.length;
  const end = nextHeading
    ? text.indexOf(nextHeading, contentStart)
    : text.length;

  return text
    .slice(contentStart, end === -1 ? text.length : end)
    .replace(/\*\*/g, "")
    .replace(/###/g, "")
    .trim();
}

export default function AIAnalysisCard({ incidents = [] }) {
  const latest = incidents[0];
  const summary = latest?.ai_summary || "";

  const rootCause = getSection(
    summary,
    "Root Cause:",
    "Business Impact:"
  );

  const impact = getSection(
    summary,
    "Business Impact:",
    "Immediate Action:"
  );

  const action = getSection(
    summary,
    "Immediate Action:",
    "Prevention:"
  );

  const prevention = getSection(
    summary,
    "Prevention:",
    "Auto-Healing Actions:"
  );

  const autoHealing = getSection(
    summary,
    "Auto-Healing Actions:",
    null
  );

  if (!latest) {
    return (
      <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold">Latest AI Analysis</h2>
        <p className="mt-4 text-slate-500">
          No AI analysis available.
        </p>
      </div>
    );
  }

  const sections = [
    ["Root Cause", rootCause],
    ["Business Impact", impact],
    ["Immediate Action", action],
    ["Prevention", prevention],
    ["Auto-Healing Actions", autoHealing],
  ];

  return (
    <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h2 className="text-xl font-bold">Latest AI Analysis</h2>
        <p className="mt-1 text-sm text-slate-500">{latest.title}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {sections.map(([title, content]) => (
          <div
            key={title}
            className="rounded-xl border border-slate-200 bg-slate-50 p-4"
          >
            <h3 className="font-semibold text-slate-900">{title}</h3>

            <p className="mt-2 whitespace-pre-line text-sm leading-6 text-slate-600">
              {content || "No details available."}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}