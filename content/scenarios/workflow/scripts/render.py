from jinja2 import Template
import yaml
import subprocess as sp
from itertools import product

meta = yaml.load(open(snakemake.input.meta, "r"), Loader=yaml.FullLoader)

plot_prior = meta.get("plot-prior", False)
print(plot_prior)
prior_plots = {}
if plot_prior:
    for sample, contig in product(plot_prior["samples"], plot_prior["contigs"]):
        cmd = ["varlociraptor", "plot", "variant-calling-prior", "--sample", str(sample), "--contig", str(contig), "--scenario", snakemake.input.scenario]
        prior_plots[(sample, contig)] = sp.run(cmd, stdout=sp.PIPE, check=True, text=True).stdout

print(prior_plots)
with open(snakemake.input.template, "r") as template, open(snakemake.input.scenario, "r") as scenario, open(snakemake.output[0], "w") as out:
    print(Template(template.read()).render(scenario=scenario.read(), prior_plots=prior_plots, name=meta["name"], desc=meta["desc"]), file=out)