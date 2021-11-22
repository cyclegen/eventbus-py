import abc
import queue
import threading


class PendingPost:

    def __init__(self, subscription, event):
        self.subscription = subscription
        self.event = event


class Executor(abc.ABC):

    @abc.abstractmethod
    def enqueue(self, subscription, event):
        pass


class MainExecutor(Executor):

    def __init__(self, eventbus):
        self.bus = eventbus

    def enqueue(self, subscription, event):
        self.bus.invoke_subscriber(subscription, event)


class MainOrderExecutor(Executor):

    def __init__(self, eventbus):
        self.quit = False
        self.queue = queue.Queue()
        self.bus = eventbus
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def enqueue(self, subscription, event):
        pending_post = PendingPost(subscription, event)
        self.queue.put(pending_post)

    def run(self):
        while not self.quit:
            pending_post = self.queue.get()
            self.bus.invoke_subscriber(pending_post.subscription, pending_post.event)

    def stop(self):
        self.quit = True
