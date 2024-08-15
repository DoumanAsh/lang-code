use lang_code::{Lang, DATA};

#[test]
fn should_validate_data_lookup_alpha3() {
    for data in DATA.iter() {
        let alpha3 = data.iso639_3();
        let lang = match Lang::from_iso639_3(alpha3) {
            Some(lang) => lang,
            None => panic!("Should have alpha3='{}' in language lookup", alpha3)
        };

        let result = lang.data();
        assert_eq!(*result, *data);
    }
}

#[test]
fn should_validate_data_lookup_alpha2() {
    for data in DATA.iter() {
        let alpha1 = match data.iso639_1() {
            Some(alpha1) => alpha1,
            None => continue
        };

        let lang = match Lang::from_iso639_1(alpha1) {
            Some(lang) => lang,
            None => panic!("Should have alpha1='{}' in language lookup", alpha1)
        };

        let result = lang.data();
        assert_eq!(*result, *data);
    }
}
