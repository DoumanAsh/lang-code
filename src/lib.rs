//! Language code library
//!
//!## Features
//!
//!- `lang-name` - Adds language name to the dataset
//!
//!## Data source
//!
//!Code is generated using python library [iso639](https://github.com/LBeaudoux/iso639)

#![no_std]
#![warn(missing_docs)]
#![cfg_attr(feature = "cargo-clippy", allow(clippy::style))]

mod data;
pub use data::{Lang, DATA};

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
///Language
pub struct Language {
    #[cfg(feature = "lang-name")]
    ///Full name of the language
    ///
    ///Only available if lang-name feature is enabled
    name: &'static str,
    ///ISO639-1 2 letter code
    part1: &'static str,
    ///ISO639-3 3 letter code
    part3: &'static str,
}

impl Language {
    #[cfg(feature = "lang-name")]
    ///Full name of the language
    ///
    ///Only available if lang-name feature is enabled
    pub const fn name(&self) -> &'static str {
        self.name
    }

    ///Returns ISO639-1 2 letter code, if language has any
    pub const fn iso639_1(&self) -> Option<&'static str> {
        if self.part1.is_empty() {
            None
        } else {
            Some(self.part1)
        }
    }

    ///Returns ISO639-3 3 letter code
    pub const fn iso639_3(&self) -> &'static str {
        self.part3
    }
}
