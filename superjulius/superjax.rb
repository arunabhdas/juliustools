require 'rubygems'
require 'nokogiri'

doc = Nokogiri::HTML <<-EOHTML
<html>
  <body>
    <item>
      <time>05.04.2011 9:53:23</time>
      <iddqd>42</iddqd>
      <idkfa>woot</idkfa>
    </item>
  </body>
</html>
EOHTML

hammer = doc.at_css "time"
hammer.name = 'superjax'
doc.css("iddqd").remove
doc.css("idkfa").remove

outfile = File.new("output2.html", "w")
outfile.puts doc.to_html
outfile.close
