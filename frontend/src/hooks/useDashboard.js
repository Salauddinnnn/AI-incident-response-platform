import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export default function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const response = await api.get("/dashboard");
      return response.data;
    },
    refetchInterval: 15000,
  });
}