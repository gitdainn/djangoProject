from django.shortcuts import render, redirect

def open_news_youtube(request):
    if request.method == 'POST':
        # POST 메소드가 들어왔을 때의 처리
        # form에서 전달된 값을 확인하여 링크를 설정
        selected_news = request.POST.get('selected_news', '')

        if selected_news == 'naver':
            naver_news_link = 'https://news.naver.com/'
            return redirect(naver_news_link)
        elif selected_news == 'bbc':
            bbc_news_link = 'https://www.bbc.com/news'
            return redirect(bbc_news_link)

    # GET 요청이나 다른 메소드에 대한 처리
    # 여기에 필요한 코드 추가

    return render(request, 'news_DB/youtubeHtml.html')
