from threading import Thread, current_thread
from lesson16_17_threads_processes_and_async.helpers.custom_logger import setup_logging
from lesson16_17_threads_processes_and_async.helpers.helper_functions import work, raise_exc_with_delay


logger = setup_logging(__name__)


TIME_SLEEP = 3


logger.info(f'Start')

# Create child Thread
t1 = Thread(
    target=work,
    args=(TIME_SLEEP, ),
    name="ChildThread1"
)

# 'target' is a function/method which code will be executed in created Child thread
# 'args' is a tuple of arguments for 'target' function
# Note: all another code except the code in 'target' functions is executed in the Main thread!
logger.info(f'Thread {t1.name} is created')

# start executing of the Child thread
t1.start()

# Case 1. Join the Child thread:
# when joining the Child thread, the Main thread will wait until the Child ia completed
t1.join()

# this code line will be executed AFTER the ChildThread1 thread will be completed
logger.info(f'Waits for the {t1.name} thread!')

# Case 2. without joining the Child thread
t2 = Thread(
    target=work,
    args=(TIME_SLEEP, ),
    name="ChildThread2"
)
logger.info(f'Thread {t2.name} is created')

t2.start()

# this code line will be executed BEFORE the ChildThread2 will be completed
logger.info(f"Doesn't wait for the {t2.name} thread!")


# 3. using 'daemon' flag
t3 = Thread(
    target=raise_exc_with_delay,
    name="ChildThreadDaemon",
    args=(3, ),
    daemon=True,
)
logger.info(f'DAEMON thread {t3.name} is created')

t3.start()

# when Thread is marked as Daemon, then NOT only the Main thread doesn't for it,
# but the whole Process doesn't wait:
# In our case the Process will exit when ChildTread2 will be completed,
# and we don't see RuntimeError which raises in ChildThreadDaemon!
logger.info(f'Thread {current_thread().name} END')



