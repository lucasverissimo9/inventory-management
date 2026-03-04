import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

let accessToken: string | null ;

export const tokenStore = {
  get: () => accessToken,
  set: (token: string | null) => { accessToken = token },
  clear: () => { accessToken = null; },
};

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenStore.get();
  if (token) config.headers.Authorization = `Bearer ${token}`;

  const company_key = localStorage.getItem("activeCompanyKey");
  if (company_key) config.headers["X-COMPANY-IDENTIFIER"] = company_key;

  return config;
});
