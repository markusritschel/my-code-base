# Examples

This is an overview

```{glue} polar_plot_features
:doc: ./examples/stereographic_maps.ipynb
:alt: "Alternative title"
:figwidth: 300px
:name: "fig-boot"

This is a **caption**!
```

{ref}`reference to the figure <fig-boot>`

{glue}`./examples/stereographic_maps.ipynb::polar_plot_features`

::::{grid} 1 1 2 3
:class-container: text-left
:gutter: 3

:::{grid-item-card} Stereographic Maps
:link: examples/stereographic_maps
:link-type: doc
:class-header: bg-light

Adding features to polar plots.
{glue}`./examples/stereographic_maps.ipynb::polar_plot_features`
:::

:::{grid-item-card} Polar contour artifacts
:link: examples/z_overlap
:link-type: doc
:class-header: bg-light

Dealing with artifacts in polar contour plots.
:::
::::

```{tableofcontents}
```
