# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.0] - 2025-10-24
### Added
- English language support: Complete English text normalization with flexible number parsing
- German language support: Complete German text normalization with intelligent format detection
- Serbian brand normalization: New BrandHandler for transliteration of car brands and companies

## [0.4.0] - 2025-10-09

### Added
- Multiplication expression handler for Serbian language
- Support for normalizing multiplication patterns (9x9, 9×9, 9*9) to "puta" format
- Pattern matching for multiplication symbols (x, ×, *) between numbers without spaces

## [0.3.0] - 2025-10-02

### Added
- Measurement normalization handler that expands units such as `km/h`, `°C`, and `m²` into Serbian spoken forms for TTS, powered by a dedicated unit mapping dataset.

## [0.2.0] - 2025-09-24

### Added
- Enhanced Serbian year normalization with full grammatical case support
- Support for feminine ordinal forms (e.g., "2021." → "dve hiljade dvadeset prva.")
- Support for neuter ordinal forms (e.g., "2021. godište" → "dve hiljade dvadeset prvo godište")
- JSON data files for feminine and neuter ordinal numbers (1-31)
- Helper methods for ordinal suffix generation in all grammatical cases

### Changed
- Refactored YearHandler to handle multiple grammatical cases systematically
- Improved pattern matching to distinguish between different year formats
- Updated regex patterns to prevent overlapping matches

## [0.1.0] - 2025-09-24

### Added

- Initial commit.