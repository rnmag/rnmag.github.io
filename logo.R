library(tidyverse)
library(ragg)

n <- 10^7

curva_1 <- tibble(
  curva = rep("curva1", n),
  valores = rnorm(n, .48, .01) # densidade para favicon: .47, .015
)

curva_2 <- tibble(
  curva = rep("curva2", n),
  valores = rnorm(n, .52, .01) # densidade para favicon: .53, .015
)

bind_rows(curva_1, curva_2) |>
  ggplot() +
  geom_density(aes(x = valores, fill = curva), alpha = .8) +
  scale_x_continuous(expand = c(0, 0), limits = c(.4, .6)) +
  guides(fill = "none") +
  scale_fill_manual(values = c("#cf4446", "#446aaf")) +
  theme_void()

ggsave("logo.png",
  device = agg_png,
  dpi = "retina",
  width = 480,
  height = 640,
  units = "px"
)
