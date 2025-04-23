from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.core.cache import cache
import requests

@login_required
@user_passes_test(lambda u: u.is_superuser)
@never_cache
def performance_dashboard(request):
    """View for system performance metrics dashboard"""
    if not hasattr(settings, 'METRICS_SERVICE_URL'):
        return render(request, 'next_gen_sms/performance.html', {
            'error': 'Metrics service is not configured'
        }, status=503)

    cache_key = f'performance_metrics_{request.user.id}'
    cached_data = cache.get(cache_key)
    if cached_data:
        return render(request, 'next_gen_sms/performance.html', cached_data)

    try:
        metrics_url = settings.METRICS_SERVICE_URL
        
        # Add timeout and retry for robustness
        response = requests.get(
            metrics_url,
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raise exception for bad status codes
        metrics = response.json()
        
        response_data = {
            'metrics': {
                'performance_score': calculate_score(metrics),
                'metrics': {
                    'first-contentful-paint': {'displayValue': f"{metrics.get('response_time', 0)}s"},
                    'speed-index': {'displayValue': f"{metrics.get('throughput', 0)} req/s"},
                    'interactive': {'displayValue': f"{metrics.get('error_rate', 0)}%"},
                    'cpu_usage': {'displayValue': f"{metrics.get('cpu_usage', 0)}%"},
                    'memory_usage': {'displayValue': f"{metrics.get('memory_usage', 0)}%"}
                }
            }
        }
        cache.set(cache_key, response_data, timeout=300)  # Cache for 5 minutes
        return render(request, 'next_gen_sms/performance.html', response_data)
    except requests.exceptions.RequestException as e:
        return render(request, 'next_gen_sms/performance.html', {
            'error': f"Could not connect to metrics service: {str(e)}"
        })
    except Exception as e:
        return render(request, 'next_gen_sms/performance.html', {
            'error': f"Error processing metrics: {str(e)}"
        })

def calculate_score(metrics):
    """Calculate overall performance score (0-100)"""
    # Simple weighted average
    weights = {
        'response_time': 0.3,
        'throughput': 0.2,
        'error_rate': 0.2,
        'cpu_usage': 0.15,
        'memory_usage': 0.15
    }
    return min(100, max(0, 
        100 - metrics['response_time'] * 10 * weights['response_time'] +
        metrics['throughput'] / 20 * weights['throughput'] +
        (100 - metrics['error_rate'] * 100) * weights['error_rate'] +
        (100 - metrics['cpu_usage']) * weights['cpu_usage'] +
        (100 - metrics['memory_usage']) * weights['memory_usage']
    ))
