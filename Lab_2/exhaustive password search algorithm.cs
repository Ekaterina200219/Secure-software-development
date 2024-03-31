using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PasswordCracker
{
    class Program
    {
        const string alphabet = "abcdefghijklmnopqrstuvwxyz";
        const int passwordLength = 5;
        /* этот метод генерирует список всех возможных паролей длиной 5, используя строчные буквы английского алфавита. 
         * Он принимает целочисленный аргумент , который указывает количество потоков, используемых для генерации паролей. 
         * Метод возвращает список списков, каждый внутренний список содержит пароли, которые будут обработаны одним потоком.*/
        static List<List<string>> GeneratePasswords(int numThreads)
        {
            List<List<string>> passwords = new List<List<string>>();

            for (int i = 0; i < numThreads; i++)
            {
                List<string> threadPasswords = new List<string>();
                passwords.Add(threadPasswords);
            }

            for (int i = 0; i < alphabet.Length; i++)
            {
                for (int j = 0; j < alphabet.Length; j++)
                {
                    for (int k = 0; k < alphabet.Length; k++)
                    {
                        for (int l = 0; l < alphabet.Length; l++)
                        {
                            for (int m = 0; m < alphabet.Length; m++)
                            {
                                string password = $"{alphabet[i]}{alphabet[j]}{alphabet[k]}{alphabet[l]}{alphabet[m]}";
                                int threadIndex = (i + j + k + l + m) % numThreads;
                                passwords[threadIndex].Add(password);
                            }
                        }
                    }
                }
            }

            return passwords;
        }

        static string ComputeSHA256(string input)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] bytes = Encoding.UTF8.GetBytes(input);
                byte[] hashBytes = sha256.ComputeHash(bytes);
                return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
            }
        }
        /*этот метод принимает в качестве аргументов массив хэшей SHA256 и целое число . 
         * Используя этот метод, он генерирует список паролей , а затем использует несколько потоков для вычисления хеша SHA256 каждого пароля 
         * и сравнения его с хэшами во входном массиве. Если совпадение найдено, пароль выводится на консоль вместе с соответствующим хешем. 
         * Метод также выводит время, затраченное на поиск пароля.*/
        static void BruteForcePasswords(List<string> hashes, int numThreads)
        {
            List<List<string>> passwords = GeneratePasswords(numThreads);
            int totalPasswords = passwords.Sum(list => list.Count);
            Console.WriteLine($"Начало перебора паролей {numThreads} потоков...");
            Stopwatch stopwatch = Stopwatch.StartNew();
            Parallel.For(0, numThreads, i =>
            {
                List<string> threadPasswords = passwords[i];
                int threadTotalPasswords = threadPasswords.Count;
                for (int j = 0; j < threadTotalPasswords; j++)
                {
                    string password = threadPasswords[j];
                    if (hashes.Count == 0)
                    {
                        break;
                    }
                    string passwordHash = ComputeSHA256(password);
                    for (int k = 0; k < hashes.Count; k++)
                    {
                        if (passwordHash == hashes[k])
                        {
                            Console.WriteLine($"Найден пароль для хеша {hashes[k]}: {password}");
                            Console.WriteLine($"Время подбора пароля: {stopwatch.Elapsed.TotalSeconds} секунд");
                            hashes.RemoveAt(k);
                        }
                    }
                }
            });
            stopwatch.Stop();
            //Console.WriteLine($"{stopwatch.Elapsed.TotalSeconds} seconds.");
        }

        static void Main(string[] args)
        {
            List<string> hashes = new List<string>();
            hashes.Add(
                "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad");
            hashes.Add(
                "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b");
            hashes.Add(
                "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f");
            

            Console.WriteLine("Выбор режима: (1) Однопоточный режим, (2) Многопоточный режим");
            int mode = Convert.ToInt32(Console.ReadLine());

            Console.WriteLine("Количество потоков:");
            int numThreads = Convert.ToInt32(Console.ReadLine());

            switch (mode)
            {
                case 1:
                    BruteForcePasswords(hashes, 1);
                    break;
                case 2:
                    BruteForcePasswords(hashes, numThreads);
                    break;
                default:
                    Console.WriteLine("Ошибка!");
                    break;
            }

            Console.ReadLine();
        }
    }
}
