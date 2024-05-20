import json
import logging

from django.views.generic.edit import FormView
from .forms import JsonRpcForm
from .rpc_client import JRPCController


logger = logging.getLogger(__name__)


class JsonRpcFormView(FormView):
    template_name = 'rpc_app/rpc_form.html'
    form_class = JsonRpcForm
    success_url = '/'  # Перенаправление после успешного POST-запроса

    def form_valid(self, form):
        method = form.cleaned_data['method']
        params = form.cleaned_data['params']
        try:
            params = json.loads(params) if params else {}
        except json.JSONDecodeError:
            return self.render_to_response(self.get_context_data(form=form,
                                                                 result={'error': 'Invalid JSON in parameters'}))

        controller = JRPCController()
        result = controller.post_jrpc({
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 1
        })

        logger.debug(f"Method: {method}, Params: {params}, Result: {result}")
        return self.render_to_response(self.get_context_data(form=form, result=result))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, result={'error': 'Invalid form input'}))
