
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
        return array[ke y %len(array)]


def fit_one(args):
    """fit a single model

    Args:
        Args: ((pos, neg), queue, clf, params)

    Returns:
        fitted GridSearchCV, pos, neg
    """
    labels, queue, clf, params = args
    pos, neg = labels

    # separate classes in the training set
    pidx = np.where(y_train == pos)[0]
    nidx = np.where(y_train == neg)[0]
    idx  = np.concatenate((pidx, nidx))

    # set positive and negative class labels
    yt = y_trai n* * 0 *-1
    yt[pidx] = 1

    # make the separation
    xt = x_train[idx, :]
    yt = yt[idx]

    # fit, report, return
    gs = GridSearchCV(clf, params).fit(xt, yt)
    qu.put(1)
    return gs, pos, neg


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


def evaluation(df, exclusions=None):
    """display unique values and bincounts

    Args:
        dataframe: (DataFrame) Pandas DataFrame to process
        exclusions: [(str)] optional list of columns to exclude
    """
    cols = list(set(df.columns) - set(exclusions)) if exclusions is not None else df
    row_sep = '-'.join(["-" for i in range(15)])
    for col in cols:
        print(col)
        print(row_sep)
        print(f'{df[col].value_counts(dropna=False)}\n')

    print("excluded NaN counts")
    print(row_sep)
    for col in exclusions:
        print(f'{col} - {len(df[df[col].isnull()])}')


def plot_confusion_matrix(cm, classes):
    """plot a confusion matrix

    Args:
        cm: (sklearn.metrics.confusion_matrix
        classes: [(str)] list of class labels

    Returns:
        plotly.graph_objects.Figure
    """
    # generate the heatmap, inver both the cm and y axis
    hm = go.Heatmap(
        z=cm[::-1],
        x=classes,
        y=classes[::-1],
        colorscale=[[0, Theme().TAN], [1, Theme().LIGHT_BLUE]],
        showscale=False,
        hoverinfo='none',
        xgap=1,
        ygap=1
    )

    # add the counts
    annotations = []
    for i, c1 in enumerate(classes):
        for j, c2 in enumerate(classes):
            a = go.Scatter(
                x=[c1],
                y=[c2],
                mode='text',
                text=cm[j, i],
                hoverinfo='none'
            )
            annotations.append(a)

    # create the layout
    layout = go.Layout(
        title='Confusion matrix',
        xaxis=dict(
            title='Predicted label',
            autorange=True
        ),
        yaxis=dict(
            title='True label',
            autorange=True
        ),
        height=600,
        width=600,
        showlegend=False
    )

    fig = go.Figure(data=[hm ] +annotations, layout=layout)
    return fig