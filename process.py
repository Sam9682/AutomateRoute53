#! /usr/bin/env python3
# coding: utf-8

import boto3
import csv
import argparse


client = boto3.client('route53')

TYPE = ['CNAME',
        'A']

ACTION = ['CREATE',
          'DELETE',
          'UPSERT']

def add_cname_record(Name, value, action, type, ttl):
   try:
      response = client.change_resource_record_sets(
         HostedZoneId='Z07614771VIQRAHF160NU',
            ChangeBatch= {
               'Comment': 'add %s -> %s' % (Name, value),
                'Changes': [
                 {
                   'Action': action,
                   'ResourceRecordSet': {
                       'Name': Name,
                       'Type': type,
                       'TTL': ttl,
                       'ResourceRecords': [{'Value': value}]
                   }
                 }]
            })
   except Exception as e:
      print(e)

def read_csv():
   try:
      with open("list_route53.csv", 'r') as file:
          csv_file = csv.DictReader(file)
          for row in csv_file:
             print(dict(row))
             add_cname_record(row["name"], row["value"], row["action"], row["type"], 300)
   except Exception as e:
      print(e)

def main():
   parser = argparse.ArgumentParser(description='Create DNS records on R53')

   parser.add_argument('-N', '--Name', required=True, type=str)
   parser.add_argument('-T', '--Type', choices=TYPE, required=True, type=str)
   parser.add_argument('-v', '--value', required=True)
   parser.add_argument('-a', '--action', choices=ACTION, required=True)
   parser.add_argument('-t', '--ttl', default=300, type=int)

   args = parser.parse_args()

   add_cname_record(args.Name, args.value, args.action, args.Type, args.ttl)

if __name__ == "__main__":
  read_csv()
