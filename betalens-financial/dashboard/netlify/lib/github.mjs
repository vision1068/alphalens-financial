// Starts BetaLens GitHub Actions jobs. Shared by the Refresh button (functions/refresh.mjs) and the
// timetable (functions/scheduler.mjs). Needs the Netlify environment variable BETALENS_GH_TOKEN: a
// fine-grained GitHub token for vision1068/alphalens-financial only, with "Actions: Read and write".
const REPO = "vision1068/alphalens-financial";
export const JOBS = { psx: "betalens-live.yml", us: "betalens-live-us.yml", daily: "betalens-daily.yml" };

const REASONS = {
  401: "GitHub rejected the key (wrong or expired). Make a new key and update BETALENS_GH_TOKEN in Netlify",
  403: "The key has no permission to run jobs. It needs Actions: Read and write on alphalens-financial",
  404: "The key cannot see the alphalens-financial repository. Give it access to that repository",
};

export function token() {
  return process.env.BETALENS_GH_TOKEN || "";
}

// Start one job unless a run of it started within `cooldownMs` or is still running.
// Returns "started", "already_running", or an error text that says what to fix.
export async function startJob(file, { cooldownMs = 4 * 60 * 1000, inputs } = {}) {
  const headers = { Authorization: `Bearer ${token()}`, Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "betalens-netlify" };
  const api = `https://api.github.com/repos/${REPO}/actions/workflows/${file}`;
  try {
    const runs = await fetch(`${api}/runs?per_page=1`, { headers });
    if (!runs.ok) return REASONS[runs.status] || `GitHub answered ${runs.status}`;
    const last = (await runs.json()).workflow_runs?.[0];
    if (last && (last.status !== "completed" || Date.now() - Date.parse(last.created_at) < cooldownMs)) {
      return "already_running";
    }
    const res = await fetch(`${api}/dispatches`, { method: "POST", headers,
      body: JSON.stringify({ ref: "main", ...(inputs ? { inputs } : {}) }) });
    return res.status === 204 ? "started" : REASONS[res.status] || `GitHub answered ${res.status}`;
  } catch (e) {
    return `Could not reach GitHub (${e.name})`;
  }
}
