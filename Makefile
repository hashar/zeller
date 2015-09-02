PYTHON = /usr/bin/env python
EXAMPLES = 20150903 20150901 20150108 20150101 20000101 15821015 15821004 15150104
PAUSED =

.PHONY: all test paused

all: test examples

%:
	@/bin/echo -n '$@ >>> ' && $(PYTHON) zeller.py "$@" || :
	@$(PAUSED)

test:
	$(PYTHON) tests.py --verbose

examples: $(EXAMPLES)
	@echo Done


paused: PAUSED = @$(shell read unused;)
paused: test examples
