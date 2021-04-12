from jinja2 import Template
import yaml
import subprocess as sp

meta = yaml.load(open(snakemake.input.meta, "r"))

plot_prior = meta.get("plot-prior", False)
prior_plots = []
if plot_prior:
    for sample in plot_prior["samples"]:
        cmd = ["varlociraptor", "plot", "variant-calling-prior", "--sample", sample, "--scenario", snakemake.input.scenario]
        contig = plot_prior.get("contig")
        if contig:
            cmd += ["--contig", contig]
        prior_plots.append(sp.run(cmd, stdout=sp.PIPE, check=True, text=True).stdout)

with open(snakemake.input.template, "r") as template, open(snakemake.input.scenario, "r") as scenario, open(snakemake.output[0], "w") as out:
    print(Template(template.read()).render(scenario=scenario.read(), prior_plots=prior_plots, name=meta["name"], desc=meta["desc"]), file=out)