# bundleID_lookup
A Python script to query http://itunes.apple.com for info related to an app bundleID

Queries data from itunes.apple.com for input bundleID(s)

Accepts -b as a single bundleID, example: com.apple.tv or a list file (one ID per line)
Accepts -k as a file list of bundleID keys (one key per line) or omit to uses the default key list
Use -s or --save to save the results to a text file

Can help identify application name, developer, website, and iTunes web address

Because lots of information can be present in the 'description' returned for an app, this information is not displayed in the results.
