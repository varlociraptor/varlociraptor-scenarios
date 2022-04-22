from jinja2 import Template
import yaml
import subprocess as sp
from itertools import product

meta = yaml.load(open(snakemake.input.meta, "r"), Loader=yaml.FullLoader)

plot_prior = meta.get("plot-prior", False)
prior_plots = {}

if plot_prior:
    samples = plot_prior["samples"]
    contigs = plot_prior["contigs"]
else:
    with open(snakemake.input.scenario, "r") as infile:
        scenario = yaml.load(infile, Loader=yaml.SafeLoader)
        samples = [next(iter(scenario["samples"].keys()))]
        contigs = ["1"]

for sample, contig in product(samples, contigs):
    cmd = ["varlociraptor", "plot", "variant-calling-prior", "--sample", str(sample), "--contig", str(contig), "--scenario", snakemake.input.scenario]
    res = sp.run(cmd, stdout=sp.PIPE, check=True, text=True)
    if plot_prior:
        prior_plots[(sample, contig)] = res.stdout

with open(snakemake.input.template, "r") as template, open(snakemake.input.scenario, "r") as scenario, open(snakemake.output[0], "w") as out:
    print(Template(template.read()).render(scenario=scenario.read(), prior_plots=prior_plots, name=meta["name"], desc=meta["desc"]), file=out)
