from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm


@login_required
def listing_list(request):
    listings = Listing.objects.filter(member=request.user.member)
    return render(request, 'listings/listing_list.html', {'listings': listings})


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.member = request.user.member
            listing.save()
            return redirect('listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/listing_create.html', {'form': form})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk, member=request.user.member)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_list')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_create.html', {'form': form})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, member=request.user.member)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})
