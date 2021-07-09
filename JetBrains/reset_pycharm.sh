for folder in ~/.config/JetBrains/PyCharm*
do
echo $folder
cd $folder
rm eval/PyCharm*.evaluation.key
rm options/other.xml
done
cd ~/.java/.userPrefs/jetbrains
rm -rf pycharm