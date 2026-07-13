import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { useState } from "react";
import { api } from "../services/api";
import { CheckCircle, AlertTriangle, XCircle, Minus, Edit, Trash2, Play, ToggleLeft, ToggleRight } from "lucide-react";

export default function Websites() {
  const queryClient = useQueryClient();
  const [deleteId, setDeleteId] = useState(null);
  const [editWebsite, setEditWebsite] = useState(null);
  const [editForm, setEditForm] = useState({ name: "", url: "" });
  const [editError, setEditError] = useState("");
  const [checkingId, setCheckingId] = useState(null);
  const [message, setMessage] = useState("");

  const {
    data: websites = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["websites"],
    queryFn: async () => {
      const response = await api.get("/websites");
      return response.data.websites || [];
    },
  });

  function showMessage(msg) {
    setMessage(msg);
    setTimeout(() => setMessage(""), 3000);
  }

  async function handleToggle(id) {
    try {
      await api.patch(`/websites/${id}/toggle`);
      queryClient.invalidateQueries({ queryKey: ["websites"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      showMessage("Website toggled successfully");
    } catch (error) {
      showMessage("Failed to toggle website");
    }
  }

  async function handleDelete(id) {
    try {
      await api.delete(`/websites/${id}`);
      queryClient.invalidateQueries({ queryKey: ["websites"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      setDeleteId(null);
      showMessage("Website deleted successfully");
    } catch (error) {
      showMessage("Failed to delete website");
    }
  }

  async function handleCheckNow(id) {
    setCheckingId(id);
    try {
      await api.post(`/websites/${id}/check`);
      queryClient.invalidateQueries({ queryKey: ["websites"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      showMessage("Check completed");
    } catch (error) {
      showMessage("Check failed");
    } finally {
      setCheckingId(null);
    }
  }

  function openEdit(website) {
    setEditWebsite(website);
    setEditForm({ name: website.name, url: website.url });
    setEditError("");
  }

  async function handleEditSubmit(event) {
    event.preventDefault();
    try {
      await api.put(`/websites/${editWebsite.id}`, editForm);
      queryClient.invalidateQueries({ queryKey: ["websites"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      setEditWebsite(null);
      showMessage("Website updated successfully");
    } catch (error) {
      setEditError(error.response?.data?.error || "Failed to update website");
    }
  }

  const statusIcon = (status) => {
    switch (status) {
      case "up":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "slow":
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case "down":
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Minus className="h-5 w-5 text-slate-400" />;
    }
  };

  if (isLoading) {
    return <p className="text-slate-500">Loading websites...</p>;
  }

  if (isError) {
    return <p className="text-red-600">Failed to load websites.</p>;
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Websites</h1>
          <p className="mt-1 text-slate-500">Manage your monitored websites</p>
        </div>

        <Link
          to="/websites/add"
          className="rounded-xl bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700"
        >
          Add Website
        </Link>
      </div>

      {message && (
        <div className="mb-4 rounded-xl bg-green-50 p-3 text-sm text-green-700">
          {message}
        </div>
      )}

      <div className="space-y-4">
        {websites.map((website) => (
          <div
            key={website.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-lg font-semibold text-slate-900">
                    {website.name}
                  </h2>
                  {statusIcon(website.current_status)}
                </div>

                <p className="mt-1 text-sm text-slate-500">{website.url}</p>

                <div className="mt-2 flex flex-wrap gap-3 text-xs text-slate-500">
                  {website.current_status && (
                    <span className="font-medium">
                      Status: {website.current_status}
                    </span>
                  )}
                  {website.status_code && (
                    <span>HTTP: {website.status_code}</span>
                  )}
                  {website.response_time_seconds && (
                    <span>Response: {website.response_time_seconds}s</span>
                  )}
                  {website.last_checked_at && (
                    <span>
                      Last checked:{" "}
                      {new Date(website.last_checked_at).toLocaleString()}
                    </span>
                  )}
                  {website.last_error && (
                    <span className="text-red-500">
                      Error: {website.last_error}
                    </span>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`w-fit rounded-full px-3 py-1 text-sm font-medium ${
                    website.is_active
                      ? "bg-green-100 text-green-700"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {website.is_active ? "Active" : "Disabled"}
                </span>

                <button
                  onClick={() => handleCheckNow(website.id)}
                  disabled={checkingId === website.id}
                  className="rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
                  title="Check Now"
                >
                  <Play className="h-4 w-4" />
                </button>

                <button
                  onClick={() => handleToggle(website.id)}
                  className="rounded-lg bg-slate-600 px-3 py-2 text-sm font-medium text-white hover:bg-slate-700"
                  title={website.is_active ? "Disable" : "Enable"}
                >
                  {website.is_active ? (
                    <ToggleRight className="h-4 w-4" />
                  ) : (
                    <ToggleLeft className="h-4 w-4" />
                  )}
                </button>

                <button
                  onClick={() => openEdit(website)}
                  className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700"
                  title="Edit"
                >
                  <Edit className="h-4 w-4" />
                </button>

                <button
                  onClick={() => setDeleteId(website.id)}
                  className="rounded-lg bg-red-600 px-3 py-2 text-sm font-medium text-white hover:bg-red-700"
                  title="Delete"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {websites.length === 0 && (
          <div className="rounded-2xl bg-white p-8 text-center text-slate-500 shadow-sm">
            No websites added yet.{" "}
            <Link to="/websites/add" className="text-blue-600 hover:underline">
              Add your first website
            </Link>
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {deleteId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="text-xl font-bold text-slate-900">
              Delete Website?
            </h2>
            <p className="mt-2 text-slate-600">
              This action cannot be undone. All associated incidents will also be
              deleted.
            </p>
            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setDeleteId(null)}
                className="rounded-lg bg-slate-100 px-4 py-2 font-medium text-slate-700 hover:bg-slate-200"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(deleteId)}
                className="rounded-lg bg-red-600 px-4 py-2 font-medium text-white hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Modal */}
      {editWebsite && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="text-xl font-bold text-slate-900">Edit Website</h2>

            <form onSubmit={handleEditSubmit} className="mt-4">
              <input
                type="text"
                placeholder="Website Name"
                value={editForm.name}
                onChange={(e) =>
                  setEditForm({ ...editForm, name: e.target.value })
                }
                className="mb-4 w-full rounded-xl border border-slate-200 p-3"
                required
              />

              <input
                type="url"
                placeholder="https://example.com"
                value={editForm.url}
                onChange={(e) =>
                  setEditForm({ ...editForm, url: e.target.value })
                }
                className="mb-4 w-full rounded-xl border border-slate-200 p-3"
                required
              />

              {editError && (
                <p className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-600">
                  {editError}
                </p>
              )}

              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setEditWebsite(null)}
                  className="rounded-lg bg-slate-100 px-4 py-2 font-medium text-slate-700 hover:bg-slate-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}