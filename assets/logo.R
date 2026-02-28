library(tidyverse)
library(ragg)
library(rstanarm)
library(bayesplot)

# logo densidades ----
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
  geom_density(aes(x = valores, fill = curva), alpha = .8, color = "#000000") +
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

# logo ppc ----
# fit <- stan_glm(gear ~ ., data = mtcars)
# posterior <- as.matrix(fit)

# color_scheme_set(c("#909090", "#909090", "#909090", 
#                    "#4d91d0", "#4d91d0", "#4d91d0"))

# ppc_dens_overlay(y = fit$y, size = .25, alpha = .2,
#                  yrep = posterior_predict(fit, draws = 750)) +
#   theme_void() + 
#   legend_none()

# ggsave("logo.png",
#   device = agg_png,
#   dpi = "retina",
#   width = 1458,
#   height = 1944,
#   units = "px"
# )
