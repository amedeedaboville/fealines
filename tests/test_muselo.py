import muselo
import mock


class TestMuse:

    def testListeners(self):
        assert muselo.server.listeners is not None  # check we have listeners (maybe move to a separate test_muselo.py?)
        plot = mock.Mock()

        muselo.server.register_listener('alpha1', plot)
        assert plot in muselo.server.listeners['alpha1']  # check we are listening to specific messages
        path = '/muse/elements/eeg'
        args = [10, 20, 30, 40]
        muselo.server.eeg_callback(path, args)
        plot.assert_called_once_with(path, args)

