import { ref, computed } from 'vue'

interface ApiError {
  userMessage?: string
  vaderQuote?: string
  isNetworkError?: boolean
  isServerError?: boolean
  isClientError?: boolean
}

interface LoadingStates {
  [key: string]: boolean
}

const loadingStates = ref<LoadingStates>({})
const errors = ref<Record<string, ApiError | null>>({})

export function useApi() {
  /**
   * Create a loading state for a specific operation
   */
  const createLoading = (key: string) => {
    const isLoading = computed(() => loadingStates.value[key] || false)
    const error = computed(() => errors.value[key] || null)
    
    const setLoading = (loading: boolean) => {
      loadingStates.value[key] = loading
      if (loading) {
        // Clear error when starting new operation
        errors.value[key] = null
      }
    }
    
    const setError = (error: ApiError | null) => {
      errors.value[key] = error
      loadingStates.value[key] = false
    }
    
    const clearError = () => {
      errors.value[key] = null
    }
    
    return {
      isLoading,
      error,
      setLoading,
      setError,
      clearError
    }
  }

  /**
   * Execute an async function with loading and error handling
   */
  const withLoading = async <T>(
    key: string,
    asyncFn: () => Promise<T>,
    options?: {
      showErrorAlert?: boolean
      fallback?: () => T | Promise<T>
    }
  ): Promise<T | null> => {
    const { setLoading, setError } = createLoading(key)
    
    try {
      setLoading(true)
      const result = await asyncFn()
      setError(null)
      return result
    } catch (error: any) {
      console.error(`API Error [${key}]:`, error)
      
      setError({
        userMessage: error.userMessage || error.message || 'An unexpected error occurred',
        vaderQuote: error.vaderQuote,
        isNetworkError: error.isNetworkError,
        isServerError: error.isServerError,
        isClientError: error.isClientError,
      })
      
      // Show error alert if requested
      if (options?.showErrorAlert) {
        const message = error.vaderQuote || error.userMessage || 'The Force is not with this request.'
        alert(`❌ ${message}`)
      }
      
      // Try fallback if provided
      if (options?.fallback) {
        try {
          return await options.fallback()
        } catch (fallbackError) {
          console.error('Fallback also failed:', fallbackError)
        }
      }
      
      return null
    } finally {
      setLoading(false)
    }
  }

  /**
   * Global loading state - true if any operation is loading
   */
  const isAnyLoading = computed(() => {
    return Object.values(loadingStates.value).some(loading => loading)
  })

  /**
   * Get all current errors
   */
  const allErrors = computed(() => {
    return Object.entries(errors.value)
      .filter(([_, error]) => error !== null)
      .reduce((acc, [key, error]) => {
        acc[key] = error!
        return acc
      }, {} as Record<string, ApiError>)
  })

  /**
   * Clear all errors
   */
  const clearAllErrors = () => {
    errors.value = {}
  }

  /**
   * Check if we have any network errors (API unavailable)
   */
  const hasNetworkError = computed(() => {
    return Object.values(errors.value).some(error => error?.isNetworkError)
  })

  return {
    createLoading,
    withLoading,
    isAnyLoading,
    allErrors,
    clearAllErrors,
    hasNetworkError,
    // Direct access to raw states if needed
    loadingStates: loadingStates.value,
    errors: errors.value,
  }
}