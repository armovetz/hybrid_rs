import magician
import sys

MAGICIAN_CONF_FILE = sys.argv[1]

Dumbledore = magician.Magician(MAGICIAN_CONF_FILE)

Dumbledore.runCrossValidation()
