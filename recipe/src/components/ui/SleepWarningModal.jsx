import Button from "./Button";

export default function SleepWarningModal({ open, onClose }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/60 backdrop-blur-sm px-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-2xl border border-gray-100">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-amber-700">
              Heads up
            </p>
            <h2 className="mt-1 text-2xl font-bold text-gray-900">
              Backend is asleep
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 6L6 18" />
              <path d="M6 6l12 12" />
            </svg>
          </button>
        </div>

        <p className="mt-3 text-sm text-gray-700 leading-relaxed">
          The backend server is currently asleep due to free tier limits.
          Your first action may take a moment while it wakes up. Thanks for
          your patience!
        </p>

        <div className="mt-6">
          <Button fullWidth onClick={onClose}>
            Got it
          </Button>
        </div>
      </div>
    </div>
  );
}

