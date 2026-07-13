import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      await api.post("/register", form);

      alert("Account Created Successfully");

      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.error || "Registration Failed");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="w-[420px] rounded-2xl bg-white p-8 shadow"
      >
        <h1 className="mb-8 text-3xl font-bold">
          Create Account
        </h1>

        <input
          placeholder="Full Name"
          className="mb-4 w-full rounded-xl border p-3"
          value={form.name}
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />

        <input
          placeholder="Email"
          className="mb-4 w-full rounded-xl border p-3"
          value={form.email}
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="Password"
          className="mb-6 w-full rounded-xl border p-3"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
        />

        <button className="w-full rounded-xl bg-blue-600 py-3 text-white">
          Create Account
        </button>
      </form>
      <p className="mt-5 text-center text-sm text-slate-500">
  Already have an account?{" "}
  <button
    type="button"
    onClick={() => navigate("/login")}
    className="font-semibold text-blue-600"
  >
    Sign in
  </button>
</p>
    </div>
  );
}