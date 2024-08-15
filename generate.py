#!/usr/bin/env python3

import re
import csv
from iso639 import iter_langs
from unicodedata import normalize as normalize_str
from collections import namedtuple

TAB = "    "
DATA_FILE = "src/data.rs"
TEST_FILE = "src/data.rs"

def main():
    brackets = re.compile(r"\s*\(.+\)")

    Language = namedtuple("Language", ['name', 'alpha2', 'alpha3', 'enum'])
    languages = []
    language_alpha3_map = dict()
    language_alpha2_map = dict()
    for lang in iter_langs():
        alpha2 = lang.pt1
        alpha3 = lang.pt3

        if not alpha2 and not alpha3:
            continue
        # Normalize name and strip non-ASCII crap
        name = normalize_str("NFKD", brackets.sub("", lang.name)).encode("ASCII", "ignore").decode('utf-8')

        if alpha3:
            enum = alpha3.upper()

            sub_map = language_alpha3_map.get(alpha3[0], dict())
            sub_map2 = sub_map.get(alpha3[1], dict())
            sub_map2[alpha3[2]] = enum
            sub_map[alpha3[1]] = sub_map2
            language_alpha3_map[alpha3[0]] = sub_map
        else:
            continue

        if alpha2:
            sub_map = language_alpha2_map.get(alpha2[0], dict())
            sub_map[alpha2[1]] = enum
            language_alpha2_map[alpha2[0]] = sub_map

        languages.append(Language(name, alpha2, alpha3, enum))

    print("Number of languages: {}".format(len(languages)))
    with open(DATA_FILE, 'w') as output:
        output.write("use crate::Language;\n\n")

        # enum tag
        output.write("#[repr(u16)]\n")
        output.write("#[derive(Copy, Clone, PartialEq, Eq)]\n")
        output.write("///Language enumeration\n")
        output.write("pub enum Lang {\n")
        for idx, lang in enumerate(languages):
            output.write("{}///{}\n".format(TAB, lang.name))
            output.write('{}{} = {},\n'.format(TAB, lang.enum, idx))
        output.write("}\n\n")

        output.write("impl Lang {\n")

        output.write("{}///Gets reference to language data\n".format(TAB))
        output.write("{}pub fn data(&self) -> &'static Language {{\n".format(TAB))
        output.write("{0}{0}&DATA[*self as usize]\n".format(TAB))
        output.write("{}}}\n".format(TAB))

        output.write("{}///Determines language tag from ISO639-3 alpha3 code\n".format(TAB))
        output.write("{}pub const fn from_iso639_3(code: &str) -> Option<Self> {{\n".format(TAB))
        output.write("{0}{0}if code.len() != 3 {{\n".format(TAB))
        output.write("{0}{0}{0}return None;\n".format(TAB))
        output.write("{0}{0}}}\n\n".format(TAB))

        output.write("{0}{0}match code.as_bytes()[0] {{\n".format(TAB))
        for (code1, sub_map) in language_alpha3_map.items():
            output.write("{0}{0}{0}b'{1}' => match code.as_bytes()[1] {{\n".format(TAB, code1))
            for (code2, sub_map2) in sub_map.items():
                output.write("{0}{0}{0}{0}b'{1}' => match code.as_bytes()[2] {{\n".format(TAB, code2))
                for (code3, enum) in sub_map2.items():
                    output.write("{0}{0}{0}{0}{0}b'{1}' => Some(Self::{2}),\n".format(TAB, code3, enum))

                output.write("{0}{0}{0}{0}{0}_ => None,\n".format(TAB))
                output.write("{0}{0}{0}{0}}},\n".format(TAB))
            output.write("{0}{0}{0}_ => None,\n".format(TAB))
            output.write("{0}{0}{0}}},\n".format(TAB))
        output.write("{0}{0}_ => None,\n".format(TAB))
        output.write("{0}{0}}}\n".format(TAB))
        output.write("{}}}\n".format(TAB))

        output.write("{}///Determines language tag from ISO639-1 alpha2 code\n".format(TAB))
        output.write("{}pub const fn from_iso639_1(code: &str) -> Option<Self> {{\n".format(TAB))
        output.write("{0}{0}if code.len() != 2 {{\n".format(TAB))
        output.write("{0}{0}{0}return None;\n".format(TAB))
        output.write("{0}{0}}}\n\n".format(TAB))

        output.write("{0}{0}match code.as_bytes()[0] {{\n".format(TAB))
        for (code1, sub_map) in language_alpha2_map.items():
            output.write("{0}{0}{0}b'{1}' => match code.as_bytes()[1] {{\n".format(TAB, code1))
            for (code2, enum) in sub_map.items():
                output.write("{0}{0}{0}{0}b'{1}' => Some(Self::{2}),\n".format(TAB, code2, enum))
            output.write("{0}{0}{0}{0}_ => None,\n".format(TAB))
            output.write("{0}{0}{0}}},\n".format(TAB))
        output.write("{0}{0}_ => None,\n".format(TAB))
        output.write("{0}{0}}}\n".format(TAB))
        output.write("{}}}\n".format(TAB))

        output.write("}\n\n")

        # data structs
        output.write("///Language data\n")
        output.write("pub static DATA: [Language; {}] = [\n".format(len(languages)))
        for lang in languages:
            output.write("{0}Language {{\n".format(TAB))
            output.write('{0}{0}#[cfg(feature = "lang-name")]\n'.format(TAB));
            output.write('{0}{0}name: "{1}",\n'.format(TAB, lang.name));
            output.write('{0}{0}part1: "{1}",\n'.format(TAB, lang.alpha2));
            output.write('{0}{0}part3: "{1}",\n'.format(TAB, lang.alpha3));
            output.write("{0}}},\n".format(TAB))
        output.write("];\n".format(len(languages)))

if __name__ == "__main__":
    main()
