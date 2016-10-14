import cPickle as pickle
import gzip

from wfuzz.exception import FuzzException
from wfuzz.plugin_api.base import wfuzz_iterator
from wfuzz.fuzzobjects import FuzzResult
from wfuzz.plugin_api.base import BasePayload

@wfuzz_iterator
class wfuzzp(BasePayload):
    name = "wfuzzp"
    description = "Returns fuzz results' URL from a previous stored wfuzz session."
    category = ["default"]
    priority = 99

    parameters = (
        ("fn", "", True, "Filename of a valid wfuzz result file."),
        ("attr", None, False, "Attribute of fuzzresult to return. If not specified the whole object is returned."),
    )

    default_parameter = "fn"

    def __init__(self, params):
        BasePayload.__init__(self, params)

	self.__max = -1
        self.attr = self.params["attr"]
	self._it = self._gen_wfuzz(self.params["fn"])

    def __iter__(self):
	return self

    def count(self):
	return self.__max

    def next(self):
	next_item = self._it.next()

        return next_item if not self.attr else next_item.get_field(self.attr)

    def _gen_wfuzz(self, output_fn):
	try:
	    with gzip.open(output_fn, 'r+b') as output:
	    #with open(self.output_fn, 'r+b') as output:
		while 1:
		    item = pickle.load(output)
                    if not isinstance(item, FuzzResult):
                        raise FuzzException(FuzzException.FATAL, "Wrong wfuzz payload format, the read object is not a valid fuzz result.")

		    yield item
	except IOError, e:
	    raise FuzzException(FuzzException.FATAL, "Error opening wfuzz payload file. %s" % str(e))
	except EOFError:
	    raise StopIteration
