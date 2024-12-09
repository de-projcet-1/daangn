from django.shortcuts import render
from django.http import JsonResponse
from category.models import Keyword, Region


def get_region(request):
    """지역 목록 조회"""
    regions = Region.objects.all().values('id', 'district', 'town')
    response_data = list(regions)
    return JsonResponse(response_data, safe=False)

def get_keywords_by_region(request):
    """지역 별 키워드 조회"""
    region_id = request.GET.get('region_id', None)
    keywords = Keyword.objects.filter(region_id=region_id, frequency__gte=2).select_related('region')

    # 지역별로 그룹화
    region_keywords = {}
    for keyword in keywords:
        region_name = f"{keyword.region.district} {keyword.region.town}"
        if region_name not in region_keywords:
            region_keywords[region_name] = {}

        region_keywords[region_name][keyword.name] = keyword.frequency

    response_data = [
        {"region": region, "keywords": keywords}
        for region, keywords in region_keywords.items()
    ]

    return JsonResponse(response_data, safe=False)
