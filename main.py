import threading
import random
import string
import time
import sys

target_text = "To be or not to be that is the question"

text_size = len(target_text)
number_of_threads = 10
thread_size = 10000

found = threading.Event()
start_time = time.time()
progress_lock = threading.Lock()
progress_bar_length = 50


def generate_random_text(size):
    return ''.join(random.choices(string.ascii_letters + ' ', k=size))


def find_text(thread_id):
    while not found.is_set():
        generated_text = generate_random_text(text_size)
        if generated_text == target_text:
            found.set()
            elapsed_time = time.time() - start_time
            with progress_lock:
                sys.stdout.write(f"\rText found by thread {thread_id}! \nElapsed time: {elapsed_time:.2f} seconds\n {target_text}")
                sys.stdout.flush()
            break


def print_progress():
    while not found.is_set():
        elapsed_time = time.time() - start_time
        progress = (elapsed_time / (number_of_threads * 10)) * 100
        progress = min(100, int(progress))
        bar_length = int((progress / 100) * progress_bar_length)

        with progress_lock:
            sys.stdout.write(
                f"\r[{'#' * bar_length}{'.' * (progress_bar_length - bar_length)}] {progress:.2f}% Elapsed time: {elapsed_time:.2f} seconds")
            sys.stdout.flush()
        time.sleep(0.1)


threads = []
for i in range(number_of_threads):
    thread = threading.Thread(target=find_text, args=(i,))
    threads.append(thread)
    thread.start()

progress_thread = threading.Thread(target=print_progress)
progress_thread.start()

for thread in threads:
    thread.join()

found.set()
progress_thread.join()
