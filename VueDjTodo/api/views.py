import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import BaseDeleteView, BaseCreateView
from django.views.generic.list import BaseListView

from todo.models import Todo


@method_decorator(ensure_csrf_cookie, name='dispatch') # csrf token을 생성
class ApiTodoLV(BaseListView):
    model = Todo

    def render_to_response(self, context, **response_kwargs):
        todoList = list(context['object_list'].values())
        return JsonResponse(data=todoList, safe=False)


class ApiTodoDelV(BaseDeleteView):
    model = Todo

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse(data={}, status=204)


class ApiTodoCV(BaseCreateView):
    model = Todo
    fields = '__all__'  # 내부에서 form을 만들기 때문에 fields 는 필수이다.

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = json.loads(self.request.body)
        print("kwargs --- ", kwargs)
        return kwargs

    def form_valid(self, form):
        print("form_valid", form)
        self.object = form.save()
        newTodo = model_to_dict(self.object) # model을 dic type으로 변환한다.

        print(f"newTodo : {newTodo}")
        return JsonResponse(data=newTodo, status=201)

    def form_invalid(self, form):
        print("form_invalid", form)
        return JsonResponse(data=form.errors, status=400)














