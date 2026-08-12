set allow-duplicate-recipes
set allow-duplicate-variables
import? 'charms.just'

[private]
@default:
  just --list
