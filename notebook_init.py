from multiprocessing import Manager, Process, Queue
from tqdm import tqdm


proc_manager = Manager()
qu = proc_manager.Queue()


class Theme():
    """simple theme to treat as an enum
    can also be indexed

    examples:
        Theme().TAN
        Theme()[99]
    """
    DARK_BLUE  = '#00585E'
    LIGHT_BLUE = '#009494'
    TAN        = '#F5F2DC'
    GREY       = '#454445'
    ORANGE     = '#FF5729'

    def __getitem__(self, key):
        array = [
            self.DARK_BLUE,
            self.LIGHT_BLUE,
            self.TAN,
            self.GREY,
            self.ORANGE
        ]
        return array[key % len(array)]


def progress_bar(total, desc=''):
    """progress bar to track parallel events

    Args:
        total: (int) total number of tasks to complete
        desc: (str) optional title to progress bar

    Returns:
        (Process, Queue)
    """
    def track_it(total, trackq):
        idx = 0
        pbar = tqdm(total=total, desc=desc)
        while True:
            update = trackq.get()
            pbar.update(1)
            idx += 1

    trackq = proc_manager.Queue()
    p = Process(target=track_it, args=(total, trackq))
    p.start()

    return p, trackq


def prod_con_map(func, vals, n_cons):
    """parallel mapping function into producer-consumer pattern

    Args:
        func: (Function) function to apply
        vals: [Object] values to apply
        n_cons: (int) number of consumers to start

    Returns:
        [Object] list of mapped function return values
    """

    def consumer(c_qu, r_qu, func):
        """consumer, terminate on receiving 'END' flag

        Args:
            c_qu: (Queue) consumption queue
            r_qu: (Queue) results queue
        """
        while True:
            val = c_qu.get()

            if val == 'END':
                break

            rv = func(val)
            r_qu.put(rv)

        r_qu.put('END')

    # create queues to pass tasks and results
    consumption_queue = Queue()
    results_queue = Queue()

    # setup the consumers
    consumers = [
        Process(target=consumer, args=(
            consumption_queue,
            results_queue,
            func
        ))
        for i in range(n_cons)
    ]

    # start the consumption processes
    [c.start() for c in consumers]

    # dish out tasks and add the termination flag
    [consumption_queue.put(val) for val in vals]
    [consumption_queue.put('END') for c in consumers]

    # turn the results into a list
    running, brake, results = n_cons, False, []
    while not brake:
        while not results_queue.empty():
            val = results_queue.get()

            if val == 'END':
                running -= 1

                if running == 0:
                    brake = True
            else:
                results.append(val)

    # kill and delete all consumers
    [c.terminate() for c in consumers]
    del consumers

    return results
