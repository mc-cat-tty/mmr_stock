from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import Request

class MailboxView(LoginRequiredMixin, ListView):
  model = Request
  template_name = "mailbox.html"
  
  def get_queryset(self):
    queryset = (
      super().get_queryset()
        .filter(profile__user = self.request.user)
        .exclude(approved = None)
    )
    ret = frozenset(queryset)
    queryset.update(viewed = True)
    return ret
  
  def get_context_data(self, **kwargs):
    extra_content = {'pagename': 'Mailbox'}
    return super().get_context_data(**kwargs) | extra_content