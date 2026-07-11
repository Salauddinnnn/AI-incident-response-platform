import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";

export default function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const [incidents, health, metrics] = await Promise.all([
        api.get("/incidents"),
        api.get("/health-check"),
        api.get("/server-metrics"),
      ]);

      return {
        incidents: incidents.data,
        health: health.data,
        metrics: metrics.data,
      };
    },
    refetchInterval: 10000,
  });
}