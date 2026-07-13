import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";

export default function AddWebsite() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [form, setForm] = useState({
    name: "",
    url: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
  await api.post("/websites", form);

  await queryClient.invalidateQueries({
    queryKey: ["websites"],
  });

  navigate("/websites", { replace: true });
} catch (requestError) {
  setError(
    requestError.response?.data?.error ||
      "Failed to add website"
  );
} finally {
  setLoading(false);
}
  }

  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold">
        Add Website
      </h1>

      <form
        onSubmit={handleSubmit}
        className="max-w-xl rounded-2xl bg-white p-6 shadow-sm"
      >
        <input
          type="text"
          placeholder="Website Name"
          value={form.name}
          onChange={(event) =>
            setForm({
              ...form,
              name: event.target.value,
            })
          }
          className="mb-4 w-full rounded-xl border border-slate-200 p-3"
          required
        />

        <input
          type="url"
          placeholder="https://example.com"
          value={form.url}
          onChange={(event) =>
            setForm({
              ...form,
              url: event.target.value,
            })
          }
          className="mb-4 w-full rounded-xl border border-slate-200 p-3"
          required
        />

        {error && (
          <p className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-600">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white disabled:opacity-50"
        >
          {loading ? "Adding..." : "Add Website"}
        </button>
      </form>
    </div>
  );
}