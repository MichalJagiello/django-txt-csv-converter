import csv
import re

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from konwerter.forms import UploadFileForm

# Create your views here.


class MyView(View):

    LINE_REGEX = b'^\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)\| ?\r\n$'
    DATE_REGEX = b'^ *BILANS OBROT\xf3W I SALD na ([\w \.]*)\r\n$'

    def _get_parsed_txt_data(self, file):
        date = None
        for line in file:
            m = re.match(self.DATE_REGEX, line)
            if m:
                date = m.group(1)
                continue
            m = re.match(self.LINE_REGEX, line)
            if m:
                if m.group(1).strip() == b'' or (m.group(1).strip() == b'1' and m.group(2).strip() == b'2'):
                    continue
                yield (data.strip().replace(',', '.') for data in (m.group(1).decode('iso-8859-1'), '',
                       m.group(2).decode('iso-8859-1'), m.group(3).decode('iso-8859-1'),
                       m.group(4).decode('iso-8859-1'), m.group(6).decode('iso-8859-1').replace('.', ''),
                       m.group(7).decode('iso-8859-1').replace('.', ''),
                       m.group(8).decode('iso-8859-1').replace('.', ''),
                       m.group(9).decode('iso-8859-1').replace('.', ''),
                       m.group(10).decode('iso-8859-1').replace('.', ''),
                       m.group(11).decode('iso-8859-1').replace('.', ''),
                       m.group(12).decode('iso-8859-1').replace('.', ''),
                       m.group(13).decode('iso-8859-1').replace('.', ''),
                       m.group(14).decode('iso-8859-1').replace('.', ''),
                       m.group(15).decode('iso-8859-1').replace('.', ''),
                       m.group(16).decode('iso-8859-1').replace('.', ''),
                       date.decode('iso-8859-1')))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="file.csv"'

            writer = csv.writer(response, delimiter=',')
            writer.writerow(['Username', 'Email', 'Imię i nazwisko', 'Numer lokalu', 'Status lokalu', 'Powierzchnia lokalu',
                             'Bilans otwarcia / Winien', 'Bilans otwarcia / Ma', 'Obroty miesięczne / Winien',
                             'Obroty miesięczne / Ma', 'Obroty bieżące / Winien', 'Obroty bieżące / Ma',
                             'Obroty ogółem / Winien', 'Obroty ogółem / Ma', 'Saldo / Winien', 'Saldo / Ma', 'Data'])
            for parsed_data in self._get_parsed_txt_data(request.FILES['plik']):
                writer.writerow(parsed_data)
            return response
        return render(request, 'upload.html', {'form': form})

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
