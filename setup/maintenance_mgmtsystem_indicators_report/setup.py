import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        "depends_override": {
            "mgmtsystem_indicators_report": "git+https://github.com/tegin/cb-addons.git@14.0#subdirectory=setup/mgmtsystem_indicators_report"
        }
    },
)
