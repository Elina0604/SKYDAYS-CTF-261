export const isDevelopment = (): boolean => {
  return import.meta.env.VITE_DEV_MODE === 'true' || import.meta.env.DEV;
};

export const getApiBaseUrl = (): string => {
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) return envUrl;
  return '/api';
};

export const getEnvironmentInfo = () => {
  return {
    hostname: window.location.hostname,
    protocol: window.location.protocol,
    isDev: isDevelopment(),
    apiUrl: getApiBaseUrl()
  };
};
