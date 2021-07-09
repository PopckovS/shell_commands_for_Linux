for folder in ~/.config/JetBrains/PhpStorm*
do
echo $folder
cd $folder
rm eval/PhpStorm*.evaluation.key
rm options/other.xml
done
cd ~/.java/.userPrefs/jetbrains
rm -rf phpstorm