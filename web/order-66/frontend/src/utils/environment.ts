export const isDevelopment = (): boolean => {
  return window.location.hostname === 'localhost' || 
         window.location.hostname === '127.0.0.1' ||
         import.meta.env.VITE_DEV_MODE === 'true';
};

export const getApiBaseUrl = (): string => {
  if (isDevelopment()) {
    return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
  }
  return `${window.location.protocol}//${window.location.host}/api`;
};

export const getEnvironmentInfo = () => {
  return {
    hostname: window.location.hostname,
    protocol: window.location.protocol,
    isDev: isDevelopment(),
    apiUrl: getApiBaseUrl()
  };
};
