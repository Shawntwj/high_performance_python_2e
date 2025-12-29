import pstats
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent
stats_file = script_dir / "profile.stats"

p = pstats.Stats(str(stats_file))
p.sort_stats("cumulative")
# p.print_stats()
# p.print_callers()
p.print_callees()
