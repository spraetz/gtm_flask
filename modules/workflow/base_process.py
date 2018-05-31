import abc


class BaseProcess:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.workflow_states = self.get_items_to_process()

    next_status = None

    @staticmethod
    @abc.abstractmethod
    def get_items_to_process():
        return

    def process(self):
        for workflow_state in self.workflow_states:
            subscription = workflow_state.get_subscription()

            self.do_work(subscription)

            workflow_state.status = self.next_status
            workflow_state.save()

    @abc.abstractmethod
    def do_work(self, subscription):
        pass
