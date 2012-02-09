# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mysite.polls.models import Choice, Poll

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html',
            {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Poll 投票フォームを再表示します。
        return render_to_response('polls/poll_detail.html', {
            'object': p,
            'error_message': "選択肢を選んでいません。",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # ユーザが Back ボタンを押して同じフォームを提出するのを防ぐ
        # ため、POST データを処理できた場合には、必ず
        # HttpResponseRedirect を返すようにします。
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})
