from concurrent.futures import Future as _BaseFuture

class Future[T](_BaseFuture[T]): ...
