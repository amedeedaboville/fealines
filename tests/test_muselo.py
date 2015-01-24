import muselo
import mock


def test_listeners():
    assert muselo.server.listeners is not None
    plot = mock.Mock()

    path = '/muse/elements/eeg/alpha1'
    muselo.server.register_listener(path, plot)
    assert plot in muselo.server.listeners[path]

    args = [10, 20, 30, 40]
    muselo.server.receive_signal(path, args)
    plot.assert_called_once_with(path, args)

    plot.reset_mock()
    muselo.server.remove_listener(path, plot)
    muselo.server.receive_signal(path, args)
    assert not plot.called
