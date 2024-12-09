import io
from wordcloud import WordCloud
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from category.models import Keyword, Region

def get_region(request):
    """지역 목록 조회"""
    regions = Region.objects.all().values('id', 'district', 'town')
    return render(request, 'category/keyword.html', {'regions': regions})

def get_keywords_by_region(request):
    """지역별 키워드 조회"""
    region_id = request.GET.get('region_id', None)
    if not region_id:
        return JsonResponse({'error': 'region_id is required'}, status=400)

    # 해당 지역의 키워드와 빈도수 가져오기
    keywords = (
        Keyword.objects.filter(region_id=region_id, frequency__gte=2)
        .values('name', 'frequency')
    )
    keyword_data = {item['name']: item['frequency'] for item in keywords}

    return JsonResponse({'keywords': keyword_data})

def generate_wordcloud(request, region_id):
    """지역별 키워드 시각화"""
    keywords = (
        Keyword.objects.filter(region_id=region_id, frequency__gte=2)
        .values('name', 'frequency')
    )
    word_frequencies = {item['name']: item['frequency'] for item in keywords}

    font_path = '/NanumGothic-Regular.ttf'
    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color='white',
    ).generate_from_frequencies(word_frequencies)

    image = io.BytesIO()
    wordcloud.to_image().save(image, format='PNG')
    image.seek(0)

    return HttpResponse(image, content_type='image/png')
