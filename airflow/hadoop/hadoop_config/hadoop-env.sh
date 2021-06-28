# The java implementation to use. By default, this environment
# variable is REQUIRED on ALL platforms except OS X!
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_DIST_CLASSPATH=$(/usr/hadoop/bin/hadoop classpath)